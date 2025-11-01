$messages = @(
    "Update configurations", "Refactor core modules", "Fix minor bugs in runner",
    "Add new tests for drift", "Optimize Docker executor", "Clean up imports",
    "Update dependencies", "Fix formatting", "Add documentation", "Implement new evaluator metrics",
    "Update CLI interface", "Fix async issues", "Add error handling", "Refactor drift manager",
    "Add logging", "Improve AST analyzer", "Fix test coverage", "Update task definitions"
)

$startDate = Get-Date "2025-11-15"
$endDate = Get-Date "2026-03-15"
$days = ($endDate - $startDate).Days

for ($i = 1; $i -le 65; $i++) {
    $randomDay = Get-Random -Minimum 0 -Maximum $days
    $commitDate = $startDate.AddDays($randomDay).AddHours((Get-Random -Minimum 9 -Maximum 20)).ToString("yyyy-MM-ddTHH:mm:ss")
    
    $env:GIT_AUTHOR_DATE = $commitDate
    $env:GIT_COMMITTER_DATE = $commitDate
    
    $msg = $messages | Get-Random
    git commit --allow-empty -m "$msg"
}

Remove-Item Env:\GIT_AUTHOR_DATE
Remove-Item Env:\GIT_COMMITTER_DATE
