FROM public.ecr.aws/lambda/nodejs:24@sha256:a34bb31e46753aa6d8e19ea3e86029add1080c6b30377ada1268db9170d8ad52

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
