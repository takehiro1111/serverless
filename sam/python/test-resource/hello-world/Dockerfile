FROM public.ecr.aws/lambda/nodejs:24@sha256:cf160411731bb339542e275373bd272f0940b6e1e5a2e0499864aa10c6d806ce

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
