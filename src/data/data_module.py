from pytorch_lightning import LightningDataModule
from transformers import T5Tokenizer
from src.data.torch_datasets import Dataset, Collator
from src.data.data_utils import FastDataLoader
from argparse import ArgumentParser
from pathlib import Path


class T5DataModule(LightningDataModule):
    def __init__(self, **kwargs):
        super(T5DataModule, self).__init__()
        self.pretrained_module_name = kwargs.get('pretrained_module_name')
        self.train_dataset_path = Path(kwargs.get('train_dataset_path'))
        self.val_dataset_path = Path(kwargs.get('val_dataset_path'))
        self.test_dataset_path = None
        self.text_maxlength = kwargs.get('text_maxlength')
        self.answer_maxlength = kwargs.get('answer_maxlength')
        self.n_context = kwargs.get('n_context')
        self.tokenizer = None
        self.args = kwargs
        self.RANDOM_SEED = 42
    
    def prepare_data(self) -> None:
        self.tokenizer = T5Tokenizer.from_pretrained(self.pretrained_module_name)
        self.collator = Collator(self.text_maxlength, self.tokenizer, answer_maxlength=self.answer_maxlength)

    def setup(self, stage: str) -> None:
        """Not using this was supposed to split the data into train, val, and test.

        Args:
            stage (str): _description_
        """
        pass
    
    @staticmethod
    def add_model_specific_args(parent_parser):
        """
        Returns the review text and the targets of the specified item
        :param parent_parser: Application specific parser
        :return: Returns the augmented argument parser
        """
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument('--train_dataset_path', type=str, default="", help='path of train data')
        parser.add_argument('--val_dataset_path', type=str, default="", help='path of eval data')
        parser.add_argument("--batch_size", default=1, type=int, help="Batch size per GPU/CPU for training.")
        parser.add_argument("--num_workers", default=4, type=int, help="Number of workers for data loading.")

        return parser

    def generate_data_loaders(self, split) -> FastDataLoader:
        """create the test set dataLoaders
        either for train, val, or test

        """
        dataset_path = getattr(self, f"{split}_dataset_path")
        dataset = Dataset(dataset_path,
                          self.n_context)
        return FastDataLoader(dataset,
                              batch_size=self.args["batch_size"],
                              num_workers=self.args["num_workers"],
                              collate_fn=self.collator)
    
    def train_dataloader(self) -> FastDataLoader:
        return self.generate_data_loaders("train")
    
    def val_dataloader(self) -> FastDataLoader:
        return self.generate_data_loaders("val")
    
    def test_dataloader(self) -> FastDataLoader:
        # for now we are testing on the validation datasest
        return self.generate_data_loaders("val")
