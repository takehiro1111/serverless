FROM public.ecr.aws/lambda/nodejs:24@sha256:5b6805c2c93462e76f53c93c897f99e2d9b895c6802aab0a9dd003db3e9a0cc4

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
