from typing import Union, List
import numpy as np
from ..base import HyperOpt
from ..hyperspace import random_space


class RandomSearch(HyperOpt):
    def __init__(
        self,
        real: Union[dict, None] = None,
        integer: Union[dict, None] = None,
        categorical: Union[dict, None] = None,
        fixed_params: Union[dict, None] = None,
        reload_path: Union[str, None] = None,
        reload_list: Union[list, None] = None,
        refine_after: Union[None, List[int], int] = None,
        refine_top_k: Union[None, int] = 5,
    ):
        HyperOpt.__init__(self, real, integer, categorical, fixed_params,
                          reload_path, reload_list)
        self.param_range = random_space(real, integer, categorical)
        self.refine_after = refine_after
        self.refine_counter = 0
        if refine_after is not None:
            assert refine_top_k > 1
            self.refine_top_k = refine_top_k

    def ask_search(self, batch_size: int):
        """Get proposals to eval next (in batches) - Random Sampling."""
        param_batch = []
        # Sample a new configuration for each eval in the batch
        while len(param_batch) < batch_size:
            proposal_params = {}
            # Sample the parameters individually at random from the ranges
            for p_name, p_range in self.param_range.items():
                if p_range["value_type"] in ["integer", "categorical"]:
                    eval_param = np.random.choice(p_range["values"])
                    if type(eval_param) == np.int64:
                        eval_param = int(eval_param)
                elif p_range["value_type"] == "real":
                    eval_param = np.random.uniform(*p_range["values"])
                proposal_params[p_name] = eval_param

            if proposal_params not in (
                self.all_evaluated_params + param_batch
            ):
                # Add parameter proposal to the batch list
                param_batch.append(proposal_params)
            else:
                # Otherwise continue sampling proposals
                continue
        return param_batch

    def tell_search(self, batch_proposals: list, perf_measures: list):
        """Perform post-iteration clean-up by updating surrogate model."""
        # Refine search space boundaries after set of search iterations
        if self.refine_after is not None:
            if self.eval_counter == self.refine_after[self.refine_counter]:
                self.refine(self.refine_top_k)
                self.refine_counter += 1

    def refine(self, top_k: int):
        """Refine the space boundaries based on top-k performers."""
        top_k_configs, top_k_evals = self.get_best(top_k)
        # Loop over real, integer and categorical variable keys
        # Get boundaries and re-define the search space
        if self.categorical is not None:
            categorical_refined = {}
            for var in self.categorical.keys():
                top_k_var = [config[var] for config in top_k_configs]
                categorical_refined[var] = list(set(top_k_var))
        else:
            categorical_refined = None

        if self.real is not None:
            real_refined = {}
            for var in self.real.keys():
                top_k_var = [config[var] for config in top_k_configs]
                real_refined[var] = {"begin": np.min(top_k_var),
                                     "end": np.max(top_k_var)}
        else:
            real_refined = None

        if self.integer is not None:
            integer_refined = {}
            for var in self.integer.keys():
                top_k_var = [config[var] for config in top_k_configs]
                integer_refined[var] = {"begin": int(np.min(top_k_var)),
                                        "end": int(np.max(top_k_var)),
                                        "spacing": self.integer[var]["spacing"]}
        else:
            integer_refined = None

        self.param_range = random_space(real_refined,
                                        integer_refined,
                                        categorical_refined)
        print("Refined the random search space:")
        print(f"Real: {real_refined}")
        print(f"Integer: {integer_refined}")
        print(f"Categorical: {categorical_refined}")
