FROM public.ecr.aws/lambda/nodejs:24@sha256:6a2bf271bdb996645b570e35ba9ed777dfb9845b801fc7ab4ac32849d2aea3c4

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
