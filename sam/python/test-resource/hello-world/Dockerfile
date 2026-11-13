FROM public.ecr.aws/lambda/nodejs:26@sha256:ed48f62aa6877801be682494abddd5a040c6024b9b4208ac48766ddea10b7913

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
