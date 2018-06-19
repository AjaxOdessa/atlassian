import com.atlassian.jira.bc.project.component.ProjectComponentManager
import com.atlassian.jira.component.ComponentAccessor
import com.atlassian.jira.issue.Issue
import com.atlassian.jira.issue.IssueManager
import com.atlassian.jira.project.ProjectManager
import com.atlassian.jira.project.version.VersionManager

Collection<String> projects = ["XXX","YYY","ZZZ"]

IssueManager issueManager = ComponentAccessor.getIssueManager()
ProjectComponentManager projectComponentManager = ComponentAccessor.getProjectComponentManager()
ProjectManager projectManager = ComponentAccessor.getProjectManager()
VersionManager versionManager = ComponentAccessor.getVersionManager()

projects.each {
	Long projectId = projectManager.getProjectObjByKey(it)?.getId()
    if (!projectId) { return }
	projectComponentManager.deleteAllComponents(projectId)
	versionManager.deleteAllVersions(projectId)
	issueManager.getIssueIdsForProject(projectId).each {
		Issue issueToDelete = issueManager.getIssueObject(it)
		issueManager.deleteIssueNoEvent(issueToDelete)
	}
}
