FROM public.ecr.aws/lambda/nodejs:24@sha256:22d0f223b961353bf986264a03f6f126bdec2e83a92050ac199d627e79218514

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
