FROM public.ecr.aws/lambda/nodejs:24@sha256:2b06ac68059668f6d1d51e752597a65e37edf61d0615a470dfb1c17927575ce9

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
