#!/bin/bash
# Copyright (c) 2019 Carlos Hernandez
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

molecule lint && \
molecule dependency && \
molecule cleanup && \
molecule destroy && \
molecule syntax && \
molecule create && \
molecule prepare && \
molecule converge -- --skip-tags='ssl-dependency' && \
molecule converge -- --skip-tags='ssl-dependency' | grep -q 'changed=0.*failed=0' && ( exit 0 || exit 1 ) && \
molecule verify && \
molecule destroy