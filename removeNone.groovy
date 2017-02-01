import com.atlassian.jira.component.ComponentAccessor;

def customField = ComponentAccessor.getCustomFieldManager().getCustomFieldObject('customfield_XXXXX')
def config = customField.getRelevantConfig(getIssueContext())
def cleanOptions = ComponentAccessor.getOptionsManager().getOptions(config)?.findAll { it.value != null }

getFieldById("customfield_XXXXX").setFieldOptions(cleanOptions)
