import torch
from torch import nn

from transformers import (
    BertModel,
    BertPreTrainedModel,
    RobertaModel,
    RobertaPreTrainedModel,
    BartModel,
    BartPretrainedModel,
    T5Model,
    T5PreTrainedModel,
    ElectraPreTrainedModel,
    ElectraModel,
    AutoModel,
)


class BertEncoder(BertPreTrainedModel):
    def __init__(self, config):
        super(BertEncoder, self).__init__(config)

        self.bert = BertModel(config)
        self.init_weights()

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        outputs = self.bert(
            input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids
        )

        pooled_output = outputs[1]

        return pooled_output


class RoBertaEncoder(RobertaPreTrainedModel):
    def __init__(self, config):
        super(RoBertaEncoder, self).__init__(config)

        self.roberta = RobertaModel(config)
        self.init_weights()

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        outputs = self.roberta(
            input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids
        )

        pooled_output = outputs[1]

        return pooled_output


class BartEncoder(BartPretrainedModel):
    def __init__(self, config):
        super(BartEncoder, self).__init__(config)

        self.bart = BartModel(config)
        self.init_weights()

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        outputs = self.bart(
            input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids
        )

        pooled_output = outputs[1]

        return pooled_output


class T5Encoder(T5PreTrainedModel):
    def __init__(self, config):
        super(T5Encoder, self).__init__(config)

        self.t5 = T5Model(config)
        self.init_weights()

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        outputs = self.t5(
            input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids
        )

        pooled_output = outputs[1]

        return pooled_output


class ElectraPooler(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.activation = nn.Tanh()

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        first_token_tensor = hidden_states[:, 0]
        pooled_output = self.dense(first_token_tensor)
        pooled_output = self.activation(pooled_output)
        return pooled_output


class ElectraEncoder(ElectraPreTrainedModel):
    def __init__(self, config):
        super(ElectraEncoder, self).__init__(config)

        self.electra = ElectraModel(config)
        self.pooler = ElectraPooler(config)
        self.init_weights()

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        outputs = self.electra(
            input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids
        )

        pooled_output = self.pooler(outputs[0])

        return pooled_output


class SBertEncoder(BertPreTrainedModel):
    def __init__(self, config):
        super(SBertEncoder, self).__init__(config)

        self.bert = AutoModel.from_config(config)
        self.init_weights()

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[
            0
        ]  # First element of model_output contains all token embeddings
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )

        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        outputs = self.bert(
            input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids
        )
        pooled_output = self.mean_pooling(outputs, attention_mask)
        # pooled_output = outputs[1]
        return pooled_output
