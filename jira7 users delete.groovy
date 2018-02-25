import com.atlassian.jira.bc.user.search.UserSearchParams
import com.atlassian.jira.bc.user.search.UserSearchService
import com.atlassian.jira.component.ComponentAccessor
import com.atlassian.jira.issue.comments.CommentManager
import com.atlassian.jira.user.util.UserUtil
import groovy.sql.Sql
import java.sql.Connection
import org.apache.log4j.Logger
import org.ofbiz.core.entity.ConnectionFactory
import org.ofbiz.core.entity.DelegatorInterface
import static java.lang.Math.toIntExact

Logger log = Logger.getLogger("com.lasman.util")
log.setLevel(org.apache.log4j.Level.INFO)

def currentUser = ComponentAccessor.jiraAuthenticationContext?.getLoggedInUser()

if (currentUser) {
	def userUtil = ComponentAccessor.getUserUtil()
	def userSearchService = ComponentAccessor.getComponent(UserSearchService.class)  
	def UserSearchParams param = new UserSearchParams(true, false, true) //(allowEmptyQuery, includeActive, includeInactive)
	def users = userSearchService.findUsers("", param)
	def delegator = (DelegatorInterface) ComponentAccessor.getComponent(DelegatorInterface)
	String helperName = delegator.getGroupHelperName("default")
	Connection dbconn = ConnectionFactory.getConnection(helperName)
	Sql request = new Sql(dbconn)
	Integer i = 0
	users.each {
		i++
		try {
			if (currentUser != it) {
				Long comments = 0
				request.eachRow("select count(id) from jiraaction where actiontype='comment' and (author=? or updateauthor=?)", [it.getName(), it.getName()]) { comments = toIntExact(it['count']) }
				if (userUtil.getNumberOfAssignedIssuesIgnoreSecurity(currentUser,it)) {
					log.warn("User $it could not be removed because there are assigned issues!")
				} else if (userUtil.getNumberOfReportedIssuesIgnoreSecurity(currentUser,it)) {
					log.warn("User $it could not be removed because there are reported issues!")
				} else if (userUtil.getComponentsUserLeads(it)) {
					log.warn("User $it could not be removed because leads a component!")
				} else if (comments > 0) {
					log.warn("User $it could not be removed because has comments")
				} else {
					userUtil.removeUser(currentUser, it)
					log.info("User ${it.getName()} successfully deleted.")
				}
			} else {
				log.info("Skipping current user ${currentUser.getName()}")
			}
		}
		catch (e) {
			log.error(e.getLocalizedMessage())
		}
		if (i%50==0) { log.info("$i users processed.") }
	}
	request.close()
}
