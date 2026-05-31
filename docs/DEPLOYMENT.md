# TitanOS Deployment Guide

## Overview

This guide describes how to deploy TitanOS in various environments.

---

## 1. Local Development

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/tianxv1/TitanOS.git
cd TitanOS
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Run Development Servers**

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

5. **Access Application**
- API: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

---

## 2. Docker Compose

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### Quick Start

1. **Create docker-compose.yml**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./database/titanos.db
      - ENV=production
    volumes:
      - ./backend/database:/app/database
    depends_on:
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

2. **Run with Docker Compose**
```bash
docker compose up -d
```

3. **Access Application**
- API: `http://localhost:8000`
- Frontend: `http://localhost:3000`

4. **Stop Services**
```bash
docker compose down
```

---

## 3. Linux Server Deployment

### Prerequisites

- Ubuntu 22.04 LTS
- sudo privileges

### Step 1: Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Dependencies
```bash
sudo apt install -y python3.9 python3.9-venv python3.9-dev \
    nginx redis-server supervisor
```

### Step 3: Clone Repository
```bash
git clone https://github.com/tianxv1/TitanOS.git /opt/titanos
cd /opt/titanos
```

### Step 4: Setup Backend
```bash
cd backend
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Setup Supervisor

**Create `/etc/supervisor/conf.d/titanos.conf`:**
```ini
[program:titanos-backend]
command=/opt/titanos/backend/venv/bin/python app.py
directory=/opt/titanos/backend
user=www-data
autostart=true
autorestart=true
stdout_logfile=/var/log/titanos/backend.log
stderr_logfile=/var/log/titanos/backend.err

[program:titanos-frontend]
command=/usr/bin/npm run start
directory=/opt/titanos/frontend
user=www-data
autostart=true
autorestart=true
stdout_logfile=/var/log/titanos/frontend.log
stderr_logfile=/var/log/titanos/frontend.err
```

**Create log directory:**
```bash
sudo mkdir -p /var/log/titanos
sudo chown www-data:www-data /var/log/titanos
```

**Start Supervisor:**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start titanos-backend
sudo supervisorctl start titanos-frontend
```

### Step 6: Setup Nginx

**Create `/etc/nginx/sites-available/titanos`:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /docs/ {
        proxy_pass http://localhost:8000/docs/;
    }
}
```

**Enable Site:**
```bash
sudo ln -s /etc/nginx/sites-available/titanos /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 7: SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 4. Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (Minikube, Kind, or production cluster)
- kubectl configured

### Step 1: Create Namespace
```bash
kubectl create namespace titanos
```

### Step 2: Deployment YAML

**Create `k8s/deployment.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: titanos-backend
  namespace: titanos
spec:
  replicas: 2
  selector:
    matchLabels:
      app: titanos-backend
  template:
    metadata:
      labels:
        app: titanos-backend
    spec:
      containers:
      - name: backend
        image: titanos-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          value: "postgresql://user:password@postgres:5432/titanos"
        - name: REDIS_URL
          value: "redis://redis:6379"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: titanos-frontend
  namespace: titanos
spec:
  replicas: 2
  selector:
    matchLabels:
      app: titanos-frontend
  template:
    metadata:
      labels:
        app: titanos-frontend
    spec:
      containers:
      - name: frontend
        image: titanos-frontend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "/api"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

**Create `k8s/service.yaml`:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: titanos-backend
  namespace: titanos
spec:
  selector:
    app: titanos-backend
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: titanos-frontend
  namespace: titanos
spec:
  selector:
    app: titanos-frontend
  ports:
  - port: 80
    targetPort: 3000
  type: ClusterIP
```

**Create `k8s/ingress.yaml`:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: titanos-ingress
  namespace: titanos
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$1
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - your-domain.com
    secretName: titanos-tls
  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /api/?(.*)
        pathType: Prefix
        backend:
          service:
            name: titanos-backend
            port:
              number: 80
      - path: /?(.*)
        pathType: Prefix
        backend:
          service:
            name: titanos-frontend
            port:
              number: 80
```

### Step 3: Apply Deployments
```bash
kubectl apply -f k8s/
```

### Step 4: Scale Deployments
```bash
kubectl scale deployment titanos-backend --replicas=3 -n titanos
kubectl scale deployment titanos-frontend --replicas=3 -n titanos
```

### Step 5: Check Status
```bash
kubectl get pods -n titanos
kubectl get services -n titanos
kubectl get ingress -n titanos
```

---

## 5. Environment Variables

### Backend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./database/titanos.db` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `ENV` | Environment | `development` |
| `PORT` | API port | `8000` |
| `SECRET_KEY` | JWT secret | `secret-key-change-in-production` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_EXPIRE_MINUTES` | JWT expiry | `1440` |

### Frontend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |

---

## 6. Database Configuration

### PostgreSQL (Production)

**Environment Variable:**
```bash
DATABASE_URL=postgresql://username:password@host:port/database
```

### SQLite (Development)

**Environment Variable:**
```bash
DATABASE_URL=sqlite:///./database/titanos.db
```

### Neo4j (Optional)

**Environment Variables:**
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

### Milvus (Optional)

**Environment Variables:**
```bash
MILVUS_URI=http://localhost:19530
MILVUS_TOKEN=your-token
```

---

## 7. Health Checks

### API Health Endpoint
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "0.3.0",
  "modules": {
    "memory": "active",
    "brain": "active",
    "planner": "active",
    "skills": "active",
    "knowledge_graph": "active",
    "learning": "active",
    "digital_twin": "active",
    "rag": "active",
    "agent": "active",
    "reflection": "active",
    "knowledge_base": "active"
  }
}
```

### Kubernetes Liveness Probe
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Kubernetes Readiness Probe
```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

---

## 8. Logging

### Backend Logs
```bash
# Development
python app.py 2>&1 | tee titanos.log

# Docker
docker logs titanos-backend

# Supervisor
sudo tail -f /var/log/titanos/backend.log

# Kubernetes
kubectl logs -n titanos titanos-backend-xxx
```

### Frontend Logs
```bash
# Development
npm run dev

# Docker
docker logs titanos-frontend

# Supervisor
sudo tail -f /var/log/titanos/frontend.log

# Kubernetes
kubectl logs -n titanos titanos-frontend-xxx
```

---

## 9. Monitoring

### Prometheus Metrics (Optional)

**Add to FastAPI:**
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

**Scrape Configuration:**
```yaml
scrape_configs:
  - job_name: 'titanos'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8000']
```

---

## 10. Backup

### Database Backup
```bash
# PostgreSQL
pg_dump titanos > backup.sql

# SQLite
cp database/titanos.db backup/titanos.db.backup

# Neo4j
neo4j-admin dump --database=neo4j --to=backup/neo4j.dump
```

### Restore
```bash
# PostgreSQL
psql titanos < backup.sql

# SQLite
cp backup/titanos.db.backup database/titanos.db

# Neo4j
neo4j-admin load --from=backup/neo4j.dump --database=neo4j --force
```

---

## 11. Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
lsof -i :8000
kill -9 <PID>
```

**2. Docker Compose Build Errors**
```bash
docker compose build --no-cache
```

**3. Nginx Configuration Errors**
```bash
nginx -t
```

**4. Supervisor Service Not Starting**
```bash
supervisorctl status
supervisorctl tail titanos-backend
```

**5. Kubernetes Pods CrashLoopBackOff**
```bash
kubectl describe pod titanos-backend-xxx
kubectl logs titanos-backend-xxx
```

---

## 12. Security Best Practices

1. **Use HTTPS**: Always use SSL/TLS certificates
2. **Environment Variables**: Store secrets in environment variables, not code
3. **Firewall**: Restrict access to database ports
4. **Regular Updates**: Keep dependencies and OS updated
5. **Least Privilege**: Use minimal permissions for service accounts
6. **Backup**: Regular backups with offsite storage
7. **Monitoring**: Set up alerts for failures

---

Last Updated: 2026-05-31
