class Params:
    def __init__(self, options: dict, params: list) -> None:
        self.options = options
        self.params: list = params
        self._failed: bool = False

    def failed(self) -> bool:
        return self._failed

    def get_normal_strings(
        self,
    ) -> list:
        strs = []
        params = self.params
        for param in params:
            if not any(param.startswith(option) for option in self.options):
                strs.append(param)
        return strs

    def get_params_with_values(self) -> dict:
        results = {}
        params = self.params
        for param in params:
            for option in list(self.options.keys()):
                if param.startswith(option):
                    try:
                        eq_idx = param.find("=")
                        if eq_idx == -1:
                            print(
                                f"Invalid Usage for Parameter {option}, Usage: --{option}={self.options[option].__name__}"
                            )
                            self._failed = True
                            return {}
                        value = self.options[option](param[eq_idx + 1 :])
                        results[option.replace("--", "")] = value
                        break
                    except:
                        print(
                            f"Invalid Value For {option}. Should be {self.options[option].__name__} , Usage:  {option}={self.options[option].__name__}"
                        )
                        self._failed = True
                        return {}
        return results
