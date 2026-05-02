module.exports = {
  apps: [{
    name: 'expense-manager',
    script: 'main.py',
    interpreter: '/home/marco/Work/code/expense_manager/venv/bin/python',
    cwd: '/home/marco/Work/code/expense_manager',
    env_file: '/home/marco/Work/code/expense_manager/.env',
    autorestart: true,
    watch: false,
    max_memory_restart: '500M'
  }]
}
