#!/bin/bash

cd i-make/vue
npm run build
cd ../..
python -m imake
