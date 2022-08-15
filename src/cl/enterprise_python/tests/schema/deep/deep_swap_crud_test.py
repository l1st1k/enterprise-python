# Copyright (C) 2021-present CompatibL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import mongoengine as me

from cl.enterprise_python.core.schema.deep.deep_leg import DeepLeg
from cl.enterprise_python.core.schema.deep.deep_swap import DeepSwap


class DeepSwapTest:
    """
    Tests for DeepSwap using MongoEngine ODM and deep style of embedding.
    """

    def test_crud(self):
        """Test CRUD operations."""

        # Connect to the database
        db_name = "deep_test_write"
        connection = me.connect(db_name)

        # Drop database if exists so the test begins from scratch
        connection.drop_database(db_name)

        ccy_list = ["USD", "GBP", "JPY", "NOK", "AUD"]
        ccy_count = len(ccy_list)

        # Create swap records
        records = [
            DeepSwap(
                trade_id=f"T{i}",
                trade_type="Swap",
                legs=[
                    DeepLeg(leg_type="Fixed", leg_ccy=ccy_list[i % ccy_count]),
                    DeepLeg(leg_type="Floating", leg_ccy="EUR")
                ]
            )
            for i in range(5)
        ]

        # TODO - use bulk insert
        for record in records:
            record.save()

        # Retrieve all records
        for swap in DeepSwap.objects:
            print(swap.trade_id)

        # Drop database to clean up
        connection.drop_database(db_name)


if __name__ == "__main__":
    pytest.main([__file__])
