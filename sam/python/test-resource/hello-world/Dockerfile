FROM public.ecr.aws/lambda/nodejs:26@sha256:4938cb1860d3f6d0cbe186919631414955af53a3c4a176056237722e0c6c6e29

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
