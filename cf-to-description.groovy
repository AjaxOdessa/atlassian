#!env groovy

import com.atlassian.jira.bc.issue.search.SearchService
import com.atlassian.jira.component.ComponentAccessor
import com.atlassian.jira.jql.parser.JqlQueryParser
import com.atlassian.jira.web.bean.PagerFilter
 
def jqlQueryParser = ComponentAccessor.getComponent(JqlQueryParser.class)

def String jql = "project = PROJECT AND cf[xxxxx] IS NOT EMPTY" // reducing unnecessary results where source is empty
def query = jqlQueryParser.parseQuery(jql)

def searchService = ComponentAccessor.getComponent(SearchService.class)
def user = ComponentAccessor.getJiraAuthenticationContext().getLoggedInUser()
def results = searchService.search(user, query, PagerFilter.getUnlimitedFilter())
def issueManager = ComponentAccessor.getIssueManager()
def customFieldManager = ComponentAccessor.getCustomFieldManager()
 
def customField = customFieldManager.getCustomFieldObject("customfield_xxxxx") // Required custom field ID

results.getIssues().each { issue ->
    def mutableIssue = issueManager.getIssueObject(issue.id)
    def _cf = issue.getCustomFieldValue(customField)?.toString()
    if ((issue.description == null) && (issue.description != _cf)) {
        mutableIssue.setDescription(_cf)
    } else {
		mutableIssue.setDescription(issue.description + '\n' + _cf)
    }
    mutableIssue.store()
}