FROM public.ecr.aws/lambda/nodejs:24@sha256:04e58cbe7bef1dadb74a4223df35d9ee917663ab24c1cbb8d9010b125bfe8558

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
