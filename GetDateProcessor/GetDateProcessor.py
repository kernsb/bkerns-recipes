#!/usr/bin/python

import time

from autopkglib import Processor, ProcessorError


__all__ = ["GetDateProcessor"]

class GetDateProcessor(Processor):
    """Shared processor to return the current date."""
    description = __doc__
    input_variables = {
    }
    output_variables = {
        "GetDate": {
            "description": "The current date in format MM/DD/YYYY.",
        },
    }

    def main(self):
        self.env["GetDate"] = (time.strftime("%m/%d/%Y"))


if __name__ == '__main__':
    PROCESSOR = GetDateProcessor()
    PROCESSOR.execute_shell()
