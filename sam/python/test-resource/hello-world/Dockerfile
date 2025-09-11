FROM public.ecr.aws/lambda/nodejs:22@sha256:27f27e5754c1a7f085677ca0a29f5571cea457363283e87e6f5a8aaba562d7ef

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
