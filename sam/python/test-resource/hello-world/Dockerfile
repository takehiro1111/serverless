FROM public.ecr.aws/lambda/nodejs:20@sha256:be35d82b919dee3ead863ea74d360f82c97cef5fe975c05bd08fe57282c22858

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
