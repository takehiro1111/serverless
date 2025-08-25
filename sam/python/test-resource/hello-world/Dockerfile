FROM public.ecr.aws/lambda/nodejs:20@sha256:b1704cff5d3d4273b3471580fe4fc2f5152873bbca7227d31f5f888fff504b81

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
