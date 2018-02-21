
var skills = ["Thermal Desktop", "Star-CCM+", "Matlab", "Python"];

var bio = {
	"name" : "Nathan Cordrey",
	"age" : 28,
	"role" : "Mechanical Engineer",
	"picture" : "static/images/me.png",
	"welcomeMessage" : "Hello!",
	"skills" : skills,
	"contacts" :
	{
		"email" : "Nathan.Cordrey@gmail.com",
		"github" : "https://github.com/lVathan",
		"twitter" : "@lVathan",
		"location" : "Salisbury, MD"
	}



};



var work = {
	"jobs" : [
		{
			"employer" : "AEPLOG Inc",
			"dates" : "June 2010 - August 2012",
			"url" : "https://www.youtube.com/watch?v=Z_28SJM9NFc",
			"title" : "Design Engineer",
			"location" : "Germantown, MD",
			"description" : "Engineered and tested autonomous robot boats"
		},
		{
			"employer" : "LJT & Associates",
			"dates" : "March 2014 - May 2016",
			"url" : "http://www.ljtinc.com/",
			"title" : "Mechanical Engineer",
			"location" : "Wallops Island, VA",
			"description" : "Provided engineering support for the Wallops Flight Facility Range"
		},
		{
			"employer" : "NASA Goddard Space Flight Center",
			"dates" : "May 2016 - Present",
			"url" : "https://www.nasa.gov/centers/wallops/home",
			"title" : "Aerospace Engineer",
			"location" : "Wallops Island, VA",
			"description" : "Provide engineering support for the Wallops Flight Facility Range. Also provide thermal engineering support to balloon and small sattelite missions."
		}
	]
};



var education = {
	"schools": [
		{
		"name" : "University of Maryland",
		"degree" : "Bachelors",
		"dates" : "September 2006 - May 2010",
		"majors" : ["Mechanical Engineering"],
		"location" : "College Park, MD"
		}
	]
};

var formattedName = HTMLheaderName.replace("%data%", bio.name);
var formattedRole = HTMLheaderRole.replace("%data%", bio.role);
var formattedBioPic = HTMLbioPic.replace("%data%", bio.picture);
var formattedWelcomeMsg = HTMLwelcomeMsg.replace("%data%", bio.welcomeMessage);

var formattedContactInfo = [];
formattedContactInfo.push(HTMLemail.replace("%data%", bio.contacts.email));
formattedContactInfo.push(HTMLgithub.replace("%data%", bio.contacts.github));
formattedContactInfo.push(HTMLtwitter.replace("%data%", bio.contacts.twitter));
formattedContactInfo.push(HTMLlocation.replace("%data%", bio.contacts.location));

var formattedFooterContactInfo = [];
formattedFooterContactInfo.push(HTMLfooteremail.replace("%data%", bio.contacts.email));
formattedFooterContactInfo.push(HTMLfootergithub.replace("%data%", bio.contacts.github));
formattedFooterContactInfo.push(HTMLfootertwitter.replace("%data%", bio.contacts.twitter));



$("#header").prepend(formattedRole);
$("#header").prepend(formattedName);
$("#header").append(formattedBioPic);
$("#header").append(formattedWelcomeMsg);


if (bio.skills.length > 0){
	$("#header").append(HTMLskillsStart);
	for (skill in bio.skills){
	var formattedSkill = HTMLskills.replace("%data%", bio.skills[skill]);
	$("#skills").append(formattedSkill)
	}

}

for(i in formattedContactInfo){
	$("#topContacts").append(formattedContactInfo[i]);
}
for(i in formattedFooterContactInfo){
	$("#footerContacts").append(formattedFooterContactInfo[i]);
}

work.display = function(){
	if (work.jobs.length > 0){
			$("#workExperience").append(HTMLworkStart);
		for (job in work.jobs){
			var formattedEmployer = HTMLworkEmployer.replace("%data%", work.jobs[job].employer);
			formattedEmployer = formattedEmployer.replace("%url%", work.jobs[job].url);
			var formattedTitle = HTMLworkTitle.replace("%data%", work.jobs[job].title);
			var formattedEmployerTitle = formattedEmployer + formattedTitle;
			var formattedWorkLocation = HTMLworkLocation.replace("%data%", work.jobs[job].location);
			var formattedDatesWorked = HTMLworkDates.replace("%data%", work.jobs[job].dates);
			var formattedWorkDescription = HTMLworkDescription.replace("%data%", work.jobs[job].description);
			$(".work-entry:last").append(formattedEmployerTitle);
			$(".work-entry:last").append(formattedWorkLocation);
			$(".work-entry:last").append(formattedDatesWorked);
			$(".work-entry:last").append(formattedWorkDescription);
		}
	}
}

work.display();

education.display = function(){
	if (education.schools.length > 0){
		for (i in education.schools){
			$("#education").append(HTMLschoolStart);

			var formattedSchoolName = HTMLschoolName.replace("%data%", education.schools[i].name);
			var formattedSchoolDegree = HTMLschoolDegree.replace("%data%", education.schools[i].degree);
			var formattedSchoolDates = HTMLschoolDates.replace("%data%", education.schools[i].dates);
			var formattedSchoolMajor = HTMLschoolMajor.replace("%data%", education.schools[i].majors);
			var formattedSchoolLocation = HTMLschoolLocation.replace("%data%", education.schools[i].location);


			$(".education-entry:last").append(formattedSchoolName);
			$(".education-entry:last").append(formattedSchoolDates);
			$(".education-entry:last").append(formattedSchoolLocation);
			$(".education-entry:last").append(formattedSchoolMajor);
		}
	}
}

education.display();
