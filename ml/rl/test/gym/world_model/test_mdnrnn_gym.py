#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.

import json
import logging
import unittest
from typing import Dict, List

import torch
from ml.rl.test.gym.world_model.mdnrnn_gym import mdnrnn_gym


logger = logging.getLogger(__name__)

MDNRNN_CARTPOLE_JSON = "ml/rl/test/configs/mdnrnn_cartpole_v0.json"


class TestMDNRNNGym(unittest.TestCase):
    def setUp(self):
        logging.getLogger().setLevel(logging.DEBUG)

    @staticmethod
    def verify_result(result_dict: Dict[str, float], expected_top_features: List[str]):
        top_feature = max(result_dict, key=result_dict.get)
        assert top_feature in expected_top_features

    def test_mdnrnn_cartpole(self):
        with open(MDNRNN_CARTPOLE_JSON, "r") as f:
            params = json.load(f)
        _, _, feature_importance_map, feature_sensitivity_map, _ = self._test_mdnrnn(
            params, feature_importance=True, feature_sensitivity=True
        )
        self.verify_result(feature_importance_map, ["state1", "state3"])
        self.verify_result(feature_sensitivity_map, ["state1", "state3"])
        print("")

    @unittest.skipIf(not torch.cuda.is_available(), "CUDA not available")
    def test_mdnrnn_cartpole_gpu(self):
        with open(MDNRNN_CARTPOLE_JSON, "r") as f:
            params = json.load(f)
        _, _, feature_importance_map, feature_sensitivity_map, _ = self._test_mdnrnn(
            params, use_gpu=True, feature_importance=True, feature_sensitivity=True
        )
        self.verify_result(feature_importance_map, ["state1", "state3"])
        self.verify_result(feature_sensitivity_map, ["state1", "state3"])

    def _test_mdnrnn(
        self, params, use_gpu=False, feature_importance=False, feature_sensitivity=False
    ):
        return mdnrnn_gym(params, use_gpu, feature_importance, feature_sensitivity)
