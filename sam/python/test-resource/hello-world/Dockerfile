FROM public.ecr.aws/lambda/nodejs:20@sha256:57d01bc49ae81bdb9d2e8822d28631ec39b0d6c2f827d59ad13f6a2f0894fd81

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
