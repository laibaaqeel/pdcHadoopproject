#!/bin/bash
echo "=================================================="
echo "   E-Commerce Sales Analysis - Setup Script"
echo "=================================================="

echo "Step 1: Installing Java and SSH..."
sudo apt-get update -q
sudo apt-get install -y openjdk-11-jdk openjdk-17-jdk openssh-server python3-pip -q
echo "Java installed!"

echo "Step 2: Configuring SSH..."
ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa -q
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
sudo service ssh start
cat > ~/.ssh/config << 'SSHEOF'
Host localhost
  StrictHostKeyChecking no
  Port 2222
SSHEOF
echo "SSH configured!"

echo "Step 3: Downloading Hadoop..."
wget -q https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzf hadoop-3.3.6.tar.gz
sudo mv hadoop-3.3.6 /usr/local/hadoop
echo "Hadoop downloaded!"

echo "Step 4: Setting environment variables..."
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
echo 'export HADOOP_HOME=/usr/local/hadoop' >> ~/.bashrc
echo 'export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' >> ~/.bashrc
echo "Environment variables set!"

echo "Step 5: Configuring Hadoop XML files..."
sudo tee /usr/local/hadoop/etc/hadoop/core-site.xml > /dev/null <<XMLEOF
<?xml version="1.0"?>
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
XMLEOF

sudo tee /usr/local/hadoop/etc/hadoop/hdfs-site.xml > /dev/null <<XMLEOF
<?xml version="1.0"?>
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///home/codespace/hadoopdata/namenode</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///home/codespace/hadoopdata/datanode</value>
  </property>
</configuration>
XMLEOF

sudo tee /usr/local/hadoop/etc/hadoop/mapred-site.xml > /dev/null <<XMLEOF
<?xml version="1.0"?>
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>mapreduce.application.classpath</name>
    <value>\$HADOOP_HOME/share/hadoop/mapreduce/*:\$HADOOP_HOME/share/hadoop/mapreduce/lib/*</value>
  </property>
</configuration>
XMLEOF

sudo tee /usr/local/hadoop/etc/hadoop/yarn-site.xml > /dev/null <<XMLEOF
<?xml version="1.0"?>
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>localhost</value>
  </property>
</configuration>
XMLEOF

sudo bash -c 'echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh'
echo "XML files configured!"

echo "Step 6: Starting Hadoop services..."
mkdir -p /home/codespace/hadoopdata/namenode
mkdir -p /home/codespace/hadoopdata/datanode
sudo chmod -R 777 /home/codespace/hadoopdata
sudo chown -R codespace:codespace /home/codespace/hadoopdata
hdfs namenode -format -force 2>&1 | tail -3
hdfs --daemon start namenode
sleep 3
sudo chmod -R 777 /home/codespace/hadoopdata/datanode
hdfs --daemon start datanode
sleep 3
start-yarn.sh
sleep 5
echo "Hadoop services started!"
jps

echo "Step 7: Setting up Python virtual environment..."
cd /workspaces/pdcHadoopproject
python3 -m venv spark_env
source spark_env/bin/activate
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
pip install pyspark pandas faker -q
echo "Python environment ready!"

echo "=================================================="
echo "   SETUP COMPLETE! Run these commands next:"
echo "   source spark_env/bin/activate"
echo "   python3 generate_data.py"
echo "   python3 analysis.py"
echo "=================================================="
