FROM public.ecr.aws/lambda/nodejs:22@sha256:2f5163461502514ecbda7d7dc020e1abe113408486e9630e967d5fd3974f4900

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
