FROM public.ecr.aws/lambda/nodejs:22@sha256:f879a8c4f0eea36987a3564f72ca4c566fc93a7e8d9e9e68cbd79ed476b07a88

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
