class System:
    """
    A class used to encapsulate the system settings for the simulation such as the number of workers in each service and the max queue sizes.
    """

    def __init__(self):
        """
        Initializes the system settings for the simulation.
        """

        # Number of workers for the Photography service
        self.num_photography_workers = 2

        # Number of workers for the Filing and Completing the Case services
        self.num_filing_completing_workers = 3

        # Number of workers for the Expert service
        self.num_expert_workers = 2

        # Number of workers for the Complaint Submission service
        self.num_submiting_complaint_workers = 1

        # Maximum queue size for the Photography service
        self.max_photography_queue_size = 20


