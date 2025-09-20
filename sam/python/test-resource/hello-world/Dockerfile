FROM public.ecr.aws/lambda/nodejs:20@sha256:dc475702a402eb35b2a48f725bee5776469e3549f3f59d24b9dd9138e3dd6382

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
