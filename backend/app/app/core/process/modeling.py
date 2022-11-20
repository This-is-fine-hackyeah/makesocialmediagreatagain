import importlib
import io
from typing import Type

import torch
import torch.nn as nn
from transformers import XLMTokenizer, RobertaModel

import importlib.resources as pkg_resources
from app.core.process import trained


class TextFeatureExtractor(nn.Module):
    def __init__(
            self,
            tokenizer="allegro/herbert-klej-cased-tokenizer-v1",
            embed_model="allegro/herbert-klej-cased-v1"
    ):
        super().__init__()

        self.tokenizer = XLMTokenizer.from_pretrained(tokenizer)
        self.embed_model = RobertaModel.from_pretrained(embed_model, return_dict=True)

        self.eval()

    def forward(self, x):
        encoded = self.tokenizer(x, return_tensors='pt', padding=True)
        encoded = {k: v.to(next(self.parameters()).device) for k, v in encoded.items()}
        return self.embed_model(**encoded)['pooler_output'].float()


class Classifier(nn.Module):
    """https://github.com/philvec/sentimentPL"""

    def __init__(self, pretrained: str, final: Type[nn.Module] = nn.Tanh):
        super().__init__()

        self.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(768, 256), nn.LeakyReLU(),
            nn.Linear(256, 16), nn.LeakyReLU(),
            nn.Linear(16, 1), final()
        )

        fp = io.BytesIO(importlib.resources.read_binary(trained, pretrained))
        self.fc.load_state_dict(torch.load(fp))
        self.eval()

    def forward(self, x):
        return self.fc(x)

    def save(self, name: str):
        torch.save(self.fc.state_dict(), name)



