# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from streamlit import config, util
from streamlit.proto.ForwardMsg_pb2 import ForwardMsg


def populate_hash_if_needed(msg: ForwardMsg) -> None:
    """Computes and assigns the unique hash for a ForwardMsg.

    If the ForwardMsg already has a hash, this is a no-op.

    Parameters
    ----------
    msg : ForwardMsg

    """
    if msg.hash == "" and msg.WhichOneof("type") not in {"ref_hash", "initialize"}:
        # Move the message's metadata aside. It's not part of the
        # hash calculation.
        metadata = msg.metadata
        msg.ClearField("metadata")

        # Serialize the message to bytes using the deterministic serializer to
        # ensure consistent hashing.
        serialized_msg = msg.SerializeToString(deterministic=True)

        # TODO(lukasmasuch): Evaluate more optimized hashing for larger messages:
        # - Add the type element type and number of bytes to the hash.
        # - Only hash the first N bytes of the message.

        # MD5 is good enough for what we need, which is uniqueness.
        msg.hash = util.calc_md5(serialized_msg)

        # Restore metadata.
        msg.metadata.CopyFrom(metadata)

        # Set cacheable flag if above the min cached size and if its a `new_element` delta.
        msg.metadata.cacheable = (
            len(serialized_msg) >= int(config.get_option("global.minCachedMessageSize"))
            and msg.WhichOneof("type") == "delta"
            and msg.delta.WhichOneof("type") == "new_element"
        )


def create_reference_msg(msg: ForwardMsg) -> ForwardMsg:
    """Create a ForwardMsg that refers to the given message via its hash.

    The reference message will also get a copy of the source message's
    metadata.

    Parameters
    ----------
    msg : ForwardMsg
        The ForwardMsg to create the reference to.

    Returns
    -------
    ForwardMsg
        A new ForwardMsg that "points" to the original message via the
        ref_hash field.

    """
    # TODO(lukasmasuch): Log error if msg.hash is not set
    ref_msg = ForwardMsg()
    ref_msg.ref_hash = msg.hash
    ref_msg.metadata.CopyFrom(msg.metadata)
    ref_msg.metadata.cacheable = False
    return ref_msg
