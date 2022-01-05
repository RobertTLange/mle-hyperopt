from mle_hyperopt import HyperbandSearch
from mle_scheduler import MLEQueue


def main():
    """Run Hyperband"""
    strategy = HyperbandSearch(
        real={"lrate": {"begin": 1e-04, "end": 1e-02, "prior": "uniform"}},
        search_config={"max_resource": 27, "eta": 3},
        seed_id=42,
        verbose=True,
    )

    # Run a loop over successive halving instantiations w. diff. trade-offs
    for hyper_iter in range(strategy.num_hb_batches):
        configs, config_fnames = strategy.ask(store=True)
        if type(config_fnames) == str:
            config_fnames = [config_fnames]
        # Instantiate queue with jobs to run
        queue = MLEQueue(
            resource_to_run="local",
            job_filename="train_mlp.py",
            config_filenames=config_fnames,
            experiment_dir="logs_hb",
            max_running_jobs=4,
            automerge_configs=True,
            delete_config=True,
        )
        queue.run()
        # Get results and storage checkpoints
        if len(config_fnames) > 1:
            scores = [queue.log[r].stats.loss.mean[-1] for r in queue.mle_run_ids]
            ckpts = [queue.log[r].meta.model_ckpt for r in queue.mle_run_ids]
        else:
            scores = [queue.log.stats.loss.mean[-1]]
            ckpts = [queue.log.meta.model_ckpt]
        strategy.tell(configs, scores, ckpts, save=True)


if __name__ == "__main__":
    main()
