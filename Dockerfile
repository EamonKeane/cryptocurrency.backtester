FROM continuumio/anaconda3:5.0.0.1

# Numpy
RUN pip install cython
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install numpy

# TA-Lib
RUN apt-get install -y build-essential
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

ENV PROJECT_FOLDER crypto-backtest
# Install the required packages from the conda environment config file
COPY environment.yml /tmp/environment.yml
# Remove the unnecessary base packages from conda to make image smaller (all are in the project environment)
RUN conda env create -f /tmp/environment.yml

# Copy the contents of the Dockefile directory to the new container
COPY . $PROJECT_FOLDER/
# Add content root to PYTHONPATH as this is where settings.py is
#ENV PYTHONPATH /$PROJECT_FOLDER
# Add the conda environment to the path (this avoids having to do source activate in the terminal)
ENV PATH /opt/conda/envs/$PROJECT_FOLDER/bin:$PATH
#Setting pythonbuffered for logs https://docs.docker.com/compose/django/#create-a-django-project
ENV PYTHONUNBUFFERED 1
RUN pip install sql_magic
#https://github.com/ipython-contrib/jupyter_contrib_nbextensions
RUN pip install jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --system
RUN pip install matplotlib
# Change working directory to the notebook directory for interactive use
WORKDIR $PROJECT_FOLDER/examples

ENV PYTHONPATH=/crypto-backtest:/crypto-backtest/src:/crypto-backtest/src/data:crypto-backtest/gemini
EXPOSE 8888

#ENTRYPOINT ["/bin/bash"]
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]