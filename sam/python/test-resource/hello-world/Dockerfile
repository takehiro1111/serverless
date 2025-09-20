FROM public.ecr.aws/lambda/nodejs:22@sha256:13603d6efc749f9492345a97390167fa6a154a18868442ac47102ad0dafa1abd

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
