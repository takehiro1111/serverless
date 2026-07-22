FROM public.ecr.aws/lambda/nodejs:26@sha256:1bb025acd7038b819b113f74ec4c9f07c06b89e8771f3da581c8ad7fe0f0275a

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
