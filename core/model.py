import subprocess
import json
import os

class ModelInference:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_inference_output(self, image_path):
        """" Gets the output of the COC model inference.
        :param image_path: The path to base image
        :type str
        :rtype dict
        :return: The json output of the model
        """
        if not self.api_key:
            raise ValueError("API key not found. Please set the API_KEY environment variable.")

        command = [
            "inference", "infer",
            "-i", image_path,
            "-m", "th3-base-detector/1",
            "--api-key", self.api_key
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout
        output = output.replace("'", "\"")
        start_index = output.find("{\"inference_id\":")

        if start_index != -1:
            valid_json_str = output[start_index:]
            return json.loads(valid_json_str)
        else:
            raise ValueError("Valid json not found in the output.")