FROM public.ecr.aws/lambda/nodejs:24@sha256:990933a1b52ee2c2261f35aa0df88b063ea42f7d7e94102d219f812cf90efe01

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
