FROM public.ecr.aws/lambda/nodejs:24@sha256:eb9586fd5adca6b3af0938e30b4a7380806c191fca66252a78f7cd369ee0d750

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
