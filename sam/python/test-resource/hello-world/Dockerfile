FROM public.ecr.aws/lambda/nodejs:22@sha256:c297308f62470f1fc04e38a473f6abb174b31f5ba00f5733de9314d7c655d76b

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
