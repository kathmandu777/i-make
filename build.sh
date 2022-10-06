#!/bin/bash

cd imake/vue
npm run build
cd ../..
python -m imake
