# Script field which contains user object of the last commenter on the issue

import com.atlassian.jira.component.ComponentAccessor

def commentManager = ComponentAccessor.getCommentManager()
if (commentManager.getLastComment(issue)) {
	def lastCommentAuthor = commentManager.getLastComment(issue).getAuthorApplicationUser()
	return lastCommentAuthor
}
