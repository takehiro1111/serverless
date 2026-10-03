FROM public.ecr.aws/lambda/nodejs:24@sha256:b5f6c6f20c76dd64924c4d09b1e3eadd91ea59eb3279d63eb99bc9102c61f58f

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
