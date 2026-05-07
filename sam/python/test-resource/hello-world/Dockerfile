FROM public.ecr.aws/lambda/nodejs:20@sha256:6d8298867120c5d1706df152e33af0bf54130b15ffbc730c61780586da05906b

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
