FROM public.ecr.aws/lambda/python:3.11

RUN yum -y install curl wget tar gzip zlib freetype-devel
RUN yum -y install libxslt \
    gcc \
    ghostscript \
    lcms2-devel \
    libffi-devel \
    libjpeg-devel \
    libtiff-devel \
    libwebp-devel \
    make \
    openjpeg2-devel \
    sudo \
    tcl-devel \
    tk-devel \
    tkinter \
    which \
    xorg-x11-server-Xvfb \
    zlib-devel \
    java \
    ipa-gothic-fonts ipa-mincho-fonts ipa-pgothic-fonts ipa-pmincho-fonts \
    && yum clean all

RUN wget https://download.documentfoundation.org/libreoffice/stable/7.6.4/rpm/x86_64/LibreOffice_7.6.4_Linux_x86-64_rpm.tar.gz -P /opt
#COPY docker/resource/LibreOffice_7.6.4_Linux_x86-64_rpm.tar.gz /opt
RUN tar -xvzf /opt/LibreOffice_7.6.4_Linux_x86-64_rpm.tar.gz -C /opt
RUN cd /opt/LibreOffice_7.6.4.1_Linux_x86-64_rpm/RPMS; yum -y install *.rpm;
RUN yum -y install cairo
COPY ../src /var/task

CMD [ "lambda_function.lambda_handler" ]