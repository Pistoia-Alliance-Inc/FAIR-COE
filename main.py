from html import escape
import json

def define_env(env):

    @env.macro
    def dama_context(
        title="GENERIC CONTEXT DIAGRAM",
        definition="High-level description of the knowledge area",
        goals=None,
        inputs=None,
        activities=None,
        deliverables=None,
        suppliers=None,
        participants=None,
        consumers=None,
        techniques=None,
        tools=None,
        metrics=None
    ):

        goals = goals or []
        inputs = inputs or []
        activities = activities or []
        deliverables = deliverables or []
        suppliers = suppliers or []
        participants = participants or []
        consumers = consumers or []
        techniques = techniques or []
        tools = tools or []
        metrics = metrics or []

        def ul(items):
            return "<ul>" + "".join(f"<li>{escape(str(x))}</li>" for x in items) + "</ul>"

        html = f'''
<div class="dama-context">

<div class="title">{escape(title)}</div>

<div class="box">
<strong>Definition:</strong> {escape(definition)}
</div>

<div class="box goals">
<strong>Goals:</strong>
{ul(goals)}
</div>

<div class="main-grid">

<div class="inputs">
<h3>Inputs</h3>
{ul(inputs)}
</div>

<div class="activities">
<h3>Activities</h3>
{ul(activities)}
</div>

<div class="deliverables">
<h3>Deliverables</h3>
{ul(deliverables)}
</div>

</div>

<div class="roles">

<div>
<h4>Suppliers</h4>
{ul(suppliers)}
</div>

<div>
<h4>Participants</h4>
{ul(participants)}
</div>

<div>
<h4>Consumers</h4>
{ul(consumers)}
</div>

</div>

<div class="bottom-pill">

<div>
<h4>Techniques</h4>
{ul(techniques)}
</div>

<div>
<h4>Tools</h4>
{ul(tools)}
</div>

<div>
<h4>Metrics</h4>
{ul(metrics)}
</div>

</div>

</div>
'''
        return html


    @env.macro
    def dama_context_from_json(data):
        if isinstance(data, str):
            data = json.loads(data)
        return dama_context(**data)
