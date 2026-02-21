FROM public.ecr.aws/lambda/nodejs:20@sha256:b1d950b97aaedc054c6c9c5409c98cf5c8f29de370a6f344113e1aeeaa441707

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
