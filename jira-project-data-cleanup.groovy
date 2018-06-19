import com.atlassian.jira.bc.project.component.ProjectComponentManager
import com.atlassian.jira.component.ComponentAccessor
import com.atlassian.jira.project.ProjectManager
import com.atlassian.jira.project.version.VersionManager

Collection<String> projects = ["XXX","YYY","ZZZ"]

ProjectManager projectManager = ComponentAccessor.getProjectManager()
ProjectComponentManager projectComponentManager = ComponentAccessor.getProjectComponentManager()
VersionManager versionManager = ComponentAccessor.getVersionManager()

projects.each {
	Long projectId = projectManager.getProjectObjByKey(it).getId()
	projectComponentManager.deleteAllComponents(projectId)
	versionManager.deleteAllVersions(projectId)
}
