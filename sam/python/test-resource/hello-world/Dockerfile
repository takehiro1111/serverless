FROM public.ecr.aws/lambda/nodejs:24@sha256:5c86981ac1c96ac8f45e053a3be08e0b9441b3f0d3af6e0a056e01802c4a75b1

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
