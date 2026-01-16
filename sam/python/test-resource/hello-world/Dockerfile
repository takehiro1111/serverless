FROM public.ecr.aws/lambda/nodejs:24@sha256:87708790ac85bff0c6e2d63808695a53372da0bb84dc37a3b1fb81cb01a2b50a

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
