FROM public.ecr.aws/lambda/nodejs:24@sha256:fd8a916b4be965f0437e397074bd3884fa0fe48d9f47af96cac69fbc65cd243b

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
